#include "jsinteractive.h"
#include "jsdevices.h"
#include "jshardware.h"

/*JSON{
  "type" : "init",
  "generate" : "jswrap_id130_init"
}*/
void jswrap_id130_init() {
#ifdef ID130
  // set pin 6 as input disconnected with internal pulldown, needed for touch button on pin 7 to work
  // could be also set as output with value 0 but this may draw less power(?)
  // this needs to be done here in init to get BTN1 working at startup time to possibly allow skipping .bootcde
  NRF_GPIO->PIN_CNF[6]=6;
#endif
}

/*xxJSON{
  "type" : "kill",
  "generate" : "jswrap_id130_kill"
}*/
//void jswrap_id130_kill() {
//}

#ifdef SDK11_BUTTONLESS_DFU

#include "nrf_svc.h"
#include "nrf_sdm.h"

#define IRQ_ENABLED            0x01                                     /**< Field that identifies if an interrupt is enabled. */
#define MAX_NUMBER_INTERRUPTS  32                                       /**< Maximum number of interrupts available. */

static void interrupts_disable(void)
{
    uint32_t interrupt_setting_mask;
    uint32_t irq;

    // Fetch the current interrupt settings.
    interrupt_setting_mask = NVIC->ISER[0];

    // Loop from interrupt 0 for disabling of all interrupts.
    for (irq = 0; irq < MAX_NUMBER_INTERRUPTS; irq++)
    {
        if (interrupt_setting_mask & (IRQ_ENABLED << irq))
        {
            // The interrupt was enabled, hence disable it.
            NVIC_DisableIRQ((IRQn_Type)irq);
        }
    }
}
#if defined ( __GNUC__ )
static inline void bootloader_util_reset(uint32_t start_addr)
{
    __asm volatile(
        "ldr   r0, [%0]\t\n"            // Get App initial MSP for bootloader.
        "msr   msp, r0\t\n"             // Set the main stack pointer to the applications MSP.
        "ldr   r0, [%0, #0x04]\t\n"     // Load Reset handler into R0.

        "movs  r4, #0xFF\t\n"           // Move ones to R4.
        "sxtb  r4, r4\t\n"              // Sign extend R4 to obtain 0xFFFFFFFF instead of 0xFF.

        "mrs   r5, IPSR\t\n"            // Load IPSR to R5 to check for handler or thread mode.
        "cmp   r5, #0x00\t\n"           // Compare, if 0 then we are in thread mode and can continue to reset handler of bootloader.
        "bne   isr_abort\t\n"           // If not zero we need to exit current ISR and jump to reset handler of bootloader.

        "mov   lr, r4\t\n"              // Clear the link register and set to ones to ensure no return.
        "bx    r0\t\n"                  // Branch to reset handler of bootloader.

        "isr_abort:  \t\n"

        "mov   r5, r4\t\n"              // Fill with ones before jumping to reset handling. Will be popped as LR when exiting ISR. Ensures no return to application.
        "mov   r6, r0\t\n"              // Move address of reset handler to R6. Will be popped as PC when exiting ISR. Ensures the reset handler will be executed when exist ISR.
        "movs  r7, #0x21\t\n"           // Move MSB reset value of xPSR to R7. Will be popped as xPSR when exiting ISR. xPSR is 0x21000000 thus MSB is 0x21.
        "rev   r7, r7\t\n"              // Reverse byte order to put 0x21 as MSB.
        "push  {r4-r7}\t\n"             // Push everything to new stack to allow interrupt handler to fetch it on exiting the ISR.

        "movs  r4, #0x00\t\n"           // Fill with zeros before jumping to reset handling. We be popped as R0 when exiting ISR (Cleaning up of the registers).
        "movs  r5, #0x00\t\n"           // Fill with zeros before jumping to reset handling. We be popped as R1 when exiting ISR (Cleaning up of the registers).
        "movs  r6, #0x00\t\n"           // Fill with zeros before jumping to reset handling. We be popped as R2 when exiting ISR (Cleaning up of the registers).
        "movs  r7, #0x00\t\n"           // Fill with zeros before jumping to reset handling. We be popped as R3 when exiting ISR (Cleaning up of the registers).
        "push  {r4-r7}\t\n"             // Push zeros (R4-R7) to stack to prepare for exiting the interrupt routine.

        "movs  r0, #0xF9\t\n"           // Move the execution return command into register, 0xFFFFFFF9.
        "sxtb  r0, r0\t\n"              // Sign extend R0 to obtain 0xFFFFFFF9 instead of 0xF9.
        "bx    r0\t\n"                  // No return - Handler mode will be exited. Stack will be popped and execution will continue in reset handler initializing other application.
        ".align\t\n"
        :: "r" (start_addr)             // Argument list for the gcc assembly. start_addr is %0.
        :  "r0", "r4", "r5", "r6", "r7" // List of register maintained manually.
    );
}
#endif

#define BOOTLOADER_SVC_BASE     0x0     /**< The number of the lowest SVC number reserved for the bootloader. */
#define SYSTEM_SERVICE_ATT_SIZE 8       /**< Size of the system service attribute length including CRC-16 at the end. */
/**@brief The SVC numbers used by the SVC functions in the SoC library. */
enum BOOTLOADER_SVCS
{
    DFU_BLE_SVC_PEER_DATA_SET = BOOTLOADER_SVC_BASE,    /**< SVC number for the setting of peer data call. */
    BOOTLOADER_SVC_LAST
};
SVCALL(DFU_BLE_SVC_PEER_DATA_SET, uint32_t, dfu_ble_svc_peer_data_set(void * p_peer_data));


#define BOOTLOADER_DFU_START 0xB1

/*JSON{
  "type" : "staticmethod",
  "ifdef" : "SDK11_BUTTONLESS_DFU",
  "class" : "E",
  "name" : "startDFU",
  "generate" : "jswrap_espruino_enter_bootloader"
}
*/
void jswrap_espruino_enter_bootloader(){
    uint32_t err_code;
    err_code = sd_power_gpregret_set(BOOTLOADER_DFU_START);
//    APP_ERROR_CHECK(err_code);

    err_code = sd_softdevice_disable();
//    APP_ERROR_CHECK(err_code);

    err_code = sd_softdevice_vector_table_base_set(NRF_UICR->NRFFW[0]);
//    APP_ERROR_CHECK(err_code);


    NVIC_ClearPendingIRQ(SWI2_IRQn);

    interrupts_disable();

    bootloader_util_reset(NRF_UICR->NRFFW[0]);
}
#endif // SDK11_BUTONLESS_DFU